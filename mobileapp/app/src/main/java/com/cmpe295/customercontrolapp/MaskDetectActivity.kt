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
import androidx.core.view.isVisible
import com.google.gson.GsonBuilder
import com.google.gson.JsonParser
import kotlinx.android.synthetic.main.activity_maskdetect.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject
import retrofit2.Retrofit
import java.io.ByteArrayOutputStream
import java.io.File

private const val FILE_NAME = "photo.jpg"
private const val REQUEST_CODE = 42
private lateinit var photoFile: File

class MaskDetectActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        Log.d("print", "creating mask detect activity")
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_maskdetect)
        detectionResponse.visibility = View.INVISIBLE
        imageView.visibility = View.INVISIBLE
        Log.d("print", "set content view")

        btnTakePicture.setOnClickListener {
            val takePictureIntent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
            photoFile = getPhotoFile(FILE_NAME)

            val fileProvider = FileProvider.getUriForFile(
                this,
                "com.cmpe295.customercontrolapp.fileprovider",
                photoFile
            )
            takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, fileProvider)

            if (takePictureIntent.resolveActivity(this.packageManager) != null) {
                startActivityForResult(takePictureIntent, REQUEST_CODE)
            } else {
                Toast.makeText(this, "Unable to open camera", Toast.LENGTH_SHORT).show()
            }
        }

        btnStopDetection.setOnClickListener {
            val intent = Intent(this, DashboardActivity::class.java);
            startActivity(intent);
        }
    }

    private fun getPhotoFile(fileName: String): File {
        val storageDirectory = getExternalFilesDir(Environment.DIRECTORY_PICTURES)
        return File.createTempFile(fileName, ".jpg", storageDirectory)
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        if (requestCode == REQUEST_CODE && resultCode == Activity.RESULT_OK) {
            val takenImage = BitmapFactory.decodeFile(photoFile.absolutePath)
            detectMask(takenImage)
        } else {
            super.onActivityResult(requestCode, resultCode, data)
        }

    }

    private fun detectMask(image: Bitmap) {

        val baos = ByteArrayOutputStream()
        image.compress(Bitmap.CompressFormat.JPEG, 100, baos)
        val byteArrayImage: ByteArray = baos.toByteArray()
        val encodedImage: String = Base64.encodeToString(byteArrayImage, Base64.DEFAULT)

        val retrofit = Retrofit.Builder()
            .baseUrl("http://192.168.1.133:8080")
            .build()

        val service = retrofit.create(APIService::class.java)

        val params = HashMap<String?, String?>()

        params["CMPE295"] = "295"
        params["SERVICE"] = "MASK"
        params["store_id"] = Session.storeID.toString()
        params["mask_pic"] = encodedImage

        CoroutineScope(Dispatchers.IO).launch {
            val response = service.postRequest(params)

            withContext(Dispatchers.Main) {
                if (response.isSuccessful) {
                    val json = JSONObject(response.body()!!.string())
                    Log.d("print", json.toString())
                    if (json.getBoolean("REPLY")) {
                        Log.d("print", "mask, can enter")
                        detectionResponse.text = "Mask detected!"
                    } else if (json.has("QRCODE")) {
                        Log.d("print", "mask, store full")
                        detectionResponse.text = "Store is full, scan QRCODE to join virtual queue"
                        val b64 = json.getString("QRCODE")
                        val imageBytes = Base64.decode(b64, Base64.DEFAULT)
                        val decodedImage = BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.size)
                        imageView.setImageBitmap(decodedImage)
                        imageView.visibility = View.VISIBLE
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