package com.phonedock.app

import android.Manifest
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.media.projection.MediaProjectionManager
import android.os.Build
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import com.phonedock.app.connectivity.ConnectionService
import com.phonedock.app.ui.dashboard.DashboardScreen
import com.phonedock.app.ui.onboarding.OnboardingScreen
import com.phonedock.app.ui.theme.PhoneDockTheme

class MainActivity : ComponentActivity() {

    private val notificationPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) {
        // Notification access is separate from the user's MediaProjection consent.
        requestScreenCaptureConsent()
    }

    private val projectionLauncher = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == RESULT_OK && result.data != null) {
            val serviceIntent = Intent(this, ConnectionService::class.java).apply {
                action = ConnectionService.ACTION_START_PROJECTION
                putExtra(ConnectionService.EXTRA_PROJECTION_RESULT_CODE, result.resultCode)
                putExtra(ConnectionService.EXTRA_PROJECTION_DATA, result.data)
            }
            startForegroundService(serviceIntent)
        }
    }

    private fun requestNotificationPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU &&
            checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED
        ) {
            notificationPermissionLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)
        } else {
            requestScreenCaptureConsent()
        }
    }

    private fun requestScreenCaptureConsent() {
        val manager = getSystemService(Context.MEDIA_PROJECTION_SERVICE) as MediaProjectionManager
        projectionLauncher.launch(manager.createScreenCaptureIntent())
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            PhoneDockTheme {
                var showOnboarding by rememberSaveable { mutableStateOf(true) }

                if (showOnboarding) {
                    OnboardingScreen(onFinished = { showOnboarding = false })
                } else {
                    DashboardScreen(onStartProjection = { requestNotificationPermission() })
                }
            }
        }
    }
}
