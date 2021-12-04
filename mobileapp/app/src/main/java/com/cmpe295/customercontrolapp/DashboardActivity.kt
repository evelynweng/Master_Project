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
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.FileProvider
import com.cmpe295.customercontrolapp.Session.Companion.storeID
import com.google.gson.GsonBuilder
import com.google.gson.JsonParser
import kotlinx.android.synthetic.main.activity_dashboard.*
import kotlinx.android.synthetic.main.activity_register.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import retrofit2.Retrofit
import java.io.ByteArrayOutputStream
import java.io.File
import java.nio.Buffer

class DashboardActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_dashboard)

        btnDetectMode.setOnClickListener {
            startDetect()
        }

    }

    private fun startDetect() {

        val retrofit = Retrofit.Builder()
            .baseUrl("http://13.52.180.123:8080/")
            .build()

        val service = retrofit.create(APIService::class.java)
        val params = HashMap<String?, String?>()

        params["CMPE295"] = "295"
        params["SERVICE"] = "STARTDETECT"
        params["store_id"] = storeID.toString()

        CoroutineScope(Dispatchers.IO).launch {
            val response = service.postRequest(params)

            withContext(Dispatchers.Main) {
                if (response.isSuccessful) {
                    val json = JSONObject(response.body()!!.string())
                    Log.d("print", json.getString("REPLY"))
                    if (json.getBoolean("REPLY")) {
                        redirectDetect()
                    } else
                        fail()
                    Log.d("print", json.toString())
                } else {
                    Log.d("print", response.code().toString())
                    error()
                }
            }
        }
    }

    private fun redirectDetect() {
        val intent = Intent(this, MaskDetectActivity::class.java);
        startActivity(intent);
    }

    private fun fail() {
        Toast.makeText(this, "Can't start mask detection right now", Toast.LENGTH_LONG).show()
    }

    private fun error() {
        Toast.makeText(this, "Couldn't connect to server", Toast.LENGTH_LONG).show()
    }
}