package com.cmpe295.customercontrolapp

import android.app.Application

class Session : Application() {
    companion object {
        var storeID = 0
    }

    override fun onCreate() {
        super.onCreate()
    }
}