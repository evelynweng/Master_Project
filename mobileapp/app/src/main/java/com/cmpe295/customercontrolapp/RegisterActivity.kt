package com.cmpe295.customercontrolapp

import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Base64
import android.util.Log
import android.widget.Toast
import com.google.gson.GsonBuilder
import com.google.gson.JsonParser
import kotlinx.android.synthetic.main.activity_register.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import retrofit2.Retrofit
import java.io.ByteArrayOutputStream

class RegisterActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_register)

        btnRegister.setOnClickListener {
            if(editStoreName.text.isEmpty() || editPhoneNumber.text.isEmpty() || editCapacity.text.isEmpty()
                || editPassword.text.isEmpty() || editConfirmPassword.text.isEmpty()) {
                Toast.makeText(this,"All Input Fields Required", Toast.LENGTH_LONG).show()
            } else if (!editPassword.text.toString().equals(editConfirmPassword.text.toString())) {
                Toast.makeText(this, "Passwords do not match", Toast.LENGTH_LONG).show()
            } else {
                registerUser();
            }
        }

        tvLogin.setOnClickListener {
            val intent = Intent(this, MainActivity::class.java);
            startActivity(intent);
        }
    }

    private fun registerUser() {

        val retrofit = Retrofit.Builder()
            .baseUrl("http://10.0.2.2:8080/")
            .build()

        val service = retrofit.create(APIService::class.java)
        val params = HashMap<String?, String?>()

        editCapacity.text.toString()

        params["CMPE295"] = "295"
        params["SERVICE"] = "REGISTER"
        params["store_phone"] = editPhoneNumber.text.toString()
        params["store_name"] = editStoreName.text.toString()
        params["password"] = editPassword.text.toString()
        params["store_capacity"] = editCapacity.text.toString()

        CoroutineScope(Dispatchers.IO).launch {
            val response = service.postRequest(params)

            withContext(Dispatchers.Main) {
                if (response.isSuccessful) {

                    val gson = GsonBuilder().setPrettyPrinting().create()
                    val prettyJson = gson.toJson(
                        JsonParser.parseString(
                            response.body()
                                ?.string()
                        )
                    )
                    Log.d("print", prettyJson)
                } else {
                    Log.d("print", response.code().toString())
                }
            }
        }
    }

}