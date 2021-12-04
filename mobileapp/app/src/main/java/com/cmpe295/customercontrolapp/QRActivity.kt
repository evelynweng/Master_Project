package com.cmpe295.customercontrolapp

import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.os.Bundle
import android.util.Base64
import android.util.Log
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.google.mlkit.vision.barcode.Barcode
import com.google.mlkit.vision.barcode.BarcodeScanner
import com.google.mlkit.vision.barcode.BarcodeScannerOptions
import com.google.mlkit.vision.barcode.BarcodeScanning
import com.google.mlkit.vision.common.InputImage
import io.fotoapparat.Fotoapparat
import io.fotoapparat.parameter.ScaleType
import io.fotoapparat.result.BitmapPhoto
import kotlinx.android.synthetic.main.activity_maskdetect.*
import kotlinx.android.synthetic.main.activity_qr.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject
import retrofit2.Retrofit

private const val CAMERA_RQ_CODE = 101

class QRActivity : AppCompatActivity() {
    private lateinit var fotoapparat: Fotoapparat
    private lateinit var barcodeScanner: BarcodeScanner

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_qr)
        setupPermissions()

        fotoapparat = Fotoapparat.with(this)
            .into(cameraView)
            .previewScaleType(ScaleType.CenterCrop)
            .build()

        val options = BarcodeScannerOptions.Builder()
            .setBarcodeFormats(
                Barcode.FORMAT_EAN_13,
                Barcode.FORMAT_QR_CODE
            ).build()

        barcodeScanner = BarcodeScanning.getClient(options)

        btnScanQR.setOnClickListener {
            takeImage()
        }

        btnMaskDetect.setOnClickListener {
            val intent = Intent(this, MaskDetectActivity::class.java);
            startActivity(intent);
        }
    }

    override fun onStart() {
        super.onStart()
        fotoapparat.start()
    }

    override fun onStop() {
        super.onStop()
        fotoapparat.stop()
    }

    private fun takeImage() {
        fotoapparat.takePicture().toBitmap().whenAvailable {
            scanImageForBarcode(it!!)
        }
    }

    private fun scanImageForBarcode(it: BitmapPhoto) {
        val inputImage = InputImage.fromBitmap(it.bitmap, it.rotationDegrees)
        val task = barcodeScanner.process(inputImage)
        task.addOnSuccessListener { barCodesList ->
            for (barcodeObject in barCodesList) {
                val barcodeValue = barcodeObject.rawValue
                Log.d("print", barcodeValue)
                val json = JSONObject(barcodeValue) // String instance holding the above json
                val intent = Intent(this@QRActivity, MaskDetectActivity::class.java);
                checkin(json.getString("store.id"), json.getString("customer.id"))
            }
        }
        task.addOnFailureListener {
            Log.d("ERROR", "An Exception occurred")
        }
    }

    private fun checkin(store_id: String, customer_id: String) {
        val retrofit = Retrofit.Builder()
            .baseUrl("http://13.52.180.123:8080/")
            .build()

        val service = retrofit.create(APIService::class.java)

        val params = HashMap<String?, String?>()

        params["CMPE295"] = "295"
        params["SERVICE"] = "CHECKIN"
        params["store_id"] = store_id
        params["customer_id"] = customer_id

        CoroutineScope(Dispatchers.IO).launch {
            val response = service.postRequest(params)

            withContext(Dispatchers.Main) {
                if (response.isSuccessful) {
                    val json = JSONObject(response.body()!!.string())
                    Log.d("print", json.toString())
                    if (json.getBoolean("REPLY")) {
                        val customerNum = json.getInt("customer_number")
                        Log.d("print", "checkin successful")
                        val intent = Intent(this@QRActivity, MaskDetectActivity::class.java);
                        intent.putExtra("customer_number", customerNum)
                        startActivity(intent);
                    } else {
                        Log.d("print", "checkin unsuccessful")
                    }
                } else {
                    Log.d("print", response.code().toString())
                }
            }
        }
    }

    private fun setupPermissions() {
        val permission = ContextCompat.checkSelfPermission(this,
            android.Manifest.permission.CAMERA)

        if (permission != PackageManager.PERMISSION_GRANTED) {
            makeRequest()
        }
    }

    private fun makeRequest() {
        ActivityCompat.requestPermissions(this,
        arrayOf(android.Manifest.permission.CAMERA),
        CAMERA_RQ_CODE)
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        when (requestCode) {
            CAMERA_RQ_CODE -> {
                if (grantResults.isEmpty() || grantResults[0] != PackageManager.PERMISSION_GRANTED) {
                    Log.d("print", "failed")
                    Toast.makeText(this, "You need camera permission to use this", Toast.LENGTH_SHORT)
                } else {
                    Log.d("print", "success")
                }
            }
        }
    }
}