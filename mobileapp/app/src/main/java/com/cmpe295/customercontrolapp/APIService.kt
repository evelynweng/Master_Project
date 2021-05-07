package com.cmpe295.customercontrolapp

import okhttp3.RequestBody
import okhttp3.ResponseBody
import retrofit2.Response
import retrofit2.http.*

interface APIService {

    @FormUrlEncoded
    @POST("/cloudservice/")
    suspend fun postRequest(@FieldMap params: HashMap<String?, String?>): Response<ResponseBody>

}

