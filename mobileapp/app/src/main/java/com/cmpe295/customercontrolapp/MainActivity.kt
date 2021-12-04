package com.cmpe295.customercontrolapp

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject
import retrofit2.Retrofit
import com.cmpe295.customercontrolapp.Session.Companion.storeID

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        btnLogin.setOnClickListener {
            if(edPhoneNumber.text.isNotEmpty() && edPassword.text.isNotEmpty()){
                Log.d("print", "sending login request...")
                loginUser();
            }else{
                Toast.makeText(this, "Input required", Toast.LENGTH_LONG).show()
            }
        }

        tvRegister.setOnClickListener {
            val intent = Intent(this, RegisterActivity::class.java);
            startActivity(intent)
        }
    }

    private fun loginUser() {

        val retrofit = Retrofit.Builder()
            .baseUrl("http://13.52.180.123:8080/")
            .build()

        val service = retrofit.create(APIService::class.java)
        val params = HashMap<String?, String?>()

        params["CMPE295"] = "295"
        params["SERVICE"] = "LOGIN"
        params["store_phone"] = edPhoneNumber.text.toString()
        params["password"] = edPassword.text.toString()

        CoroutineScope(Dispatchers.IO).launch {
            val response = service.postRequest(params)

            withContext(Dispatchers.Main) {
                if (response.isSuccessful) {
                    val json = JSONObject(response.body()!!.string())
                    Log.d("print", json.getString("REPLY"))
                    if (json.getBoolean("REPLY")) {
                        storeID = json.getInt("store_id")
                        successfulLogin()
                    } else
                        badLogin()
                } else {
                    Log.d("print", response.code().toString())
                    error()
                }
            }
        }
    }

    private fun successfulLogin() {
        Log.d("print", storeID.toString())

        val intent = Intent(this, DashboardActivity::class.java);
        startActivity(intent);
    }

    private fun badLogin() {
        Toast.makeText(this, "Invalid Login Credentials", Toast.LENGTH_LONG).show()
    }

    private fun error() {
        Toast.makeText(this, "Couldn't connect to server", Toast.LENGTH_LONG).show()
    }

}