package com.phonedock.app

import android.content.Context
import android.content.Intent
import android.media.projection.MediaProjectionManager
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

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            PhoneDockTheme {
                var showOnboarding by rememberSaveable { mutableStateOf(true) }

                if (showOnboarding) {
                    OnboardingScreen(onFinished = { showOnboarding = false })
                } else {
                    DashboardScreen(onStartProjection = {
                        val manager = getSystemService(Context.MEDIA_PROJECTION_SERVICE) as MediaProjectionManager
                        projectionLauncher.launch(manager.createScreenCaptureIntent())
                    })
                }
            }
        }
    }
}
