package com.cmpe295.customercontrolapp

import android.app.Activity
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.os.Bundle
import android.os.Environment
import android.provider.MediaStore
import android.util.Base64
import android.util.Log
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.FileProvider
import kotlinx.android.synthetic.main.activity_maskdetect.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject
import retrofit2.Retrofit
import java.io.ByteArrayOutputStream
import java.io.File

private const val FILE_NAME = "photo1.jpg"
private const val REQUEST_CODE_MASK = 42
private const val REQUEST_CODE_CARD = 43
private lateinit var photoFile: File
private var customerNum = -1

class MaskDetectActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        customerNum = intent.getIntExtra("customer_number", -1)
        Log.d("print", customerNum.toString())
        setContentView(R.layout.activity_maskdetect)
        detectionResponse.visibility = View.INVISIBLE
        imageView.visibility = View.INVISIBLE

        btnMaskPic.setOnClickListener {
            takePicture(REQUEST_CODE_MASK)
        }

        btnVaccineCard.setOnClickListener {
            takePicture(REQUEST_CODE_CARD)
        }

        btnStopDetection.setOnClickListener {
            val intent = Intent(this, DashboardActivity::class.java);
            startActivity(intent);
        }

        btnQRScan.setOnClickListener {
            val intent = Intent(this, QRActivity::class.java);
            startActivity(intent);
        }
    }

    private fun takePicture(requestCode: Int) {
        val takePictureIntent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
        photoFile = getPhotoFile(FILE_NAME)

        val fileProvider = FileProvider.getUriForFile(
            this,
            "com.cmpe295.customercontrolapp.fileprovider",
            photoFile
        )
        takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, fileProvider)

        if (takePictureIntent.resolveActivity(this.packageManager) != null) {
            startActivityForResult(takePictureIntent, requestCode)
        } else {
            Toast.makeText(this, "Unable to open camera", Toast.LENGTH_SHORT).show()
        }
    }

    private fun getPhotoFile(fileName: String): File {
        val storageDirectory = getExternalFilesDir(Environment.DIRECTORY_PICTURES)
        return File.createTempFile(fileName, ".jpg", storageDirectory)
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        if (resultCode == Activity.RESULT_OK) {
            val takenImage = BitmapFactory.decodeFile(photoFile.absolutePath)
            imageView.setImageBitmap(takenImage)
            imageView.visibility = View.VISIBLE
            val baos = ByteArrayOutputStream()
            takenImage.compress(Bitmap.CompressFormat.JPEG, 100, baos)
            val byteArrayImage: ByteArray = baos.toByteArray()
            val encodedImage: String = Base64.encodeToString(byteArrayImage, Base64.DEFAULT)
            if (requestCode == REQUEST_CODE_MASK) {
                Log.d("print", "mask")
                sendRequest(encodedImage, "False")
            } else if (requestCode == REQUEST_CODE_CARD) {
                Log.d("print", "vaccine card")
                sendRequest(encodedImage, "True")
            }
        } else {
            super.onActivityResult(requestCode, resultCode, data)
        }

    }

    private fun sendRequest(encodedString: String, vaccineCard: String) {

        val retrofit = Retrofit.Builder()
            .baseUrl("http://13.52.180.123:8080/")
            .build()

        val service = retrofit.create(APIService::class.java)

        val params = HashMap<String?, String?>()

        params["CMPE295"] = "295"
        params["SERVICE"] = "MASK"
        params["store_id"] = Session.storeID.toString()
        params["mask_pic"] = encodedString
        params["vacc_card"] = vaccineCard

        CoroutineScope(Dispatchers.IO).launch {
            val response = service.postRequest(params)

            withContext(Dispatchers.Main) {
                if (response.isSuccessful) {

                    val json = JSONObject(response.body()!!.string())
                    Log.d("print", json.toString())
                    if (json.getBoolean("REPLY")) {
                        Log.d("print", "mask, can enter")
                        detectionResponse.text = "You may enter"
                    } else if (json.has("QRCODE")) {
                        if (json.getString("QRCODE") == "null") {
                            Log.d("print", "null qrcode no mask")
                            detectionResponse.text = "Mask not detected"
                        } else {
                            Log.d("print", "mask, store full")
                            detectionResponse.text = "Store is full, scan QRCODE to join virtual queue"
                            val b64 = json.getString("QRCODE")
                            val imageBytes = Base64.decode(b64, Base64.DEFAULT)
                            val decodedImage = BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.size)
                            imageView.setImageBitmap(decodedImage)
                            imageView.visibility = View.VISIBLE
                        }
                    } else {
                        Log.d("print", "no mask")
                        detectionResponse.text = "Mask not detected"
                    }
                } else {
                    Log.d("print", response.code().toString())
                    detectionResponse.text = "Couldn't connect to server"
                }
                detectionResponse.visibility = View.VISIBLE
            }
        }
    }
}