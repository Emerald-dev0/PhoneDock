package com.phonedock.app.connectivity

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Intent
import android.os.Build
import android.os.IBinder
import android.util.Log
import androidx.core.app.NotificationCompat
import android.app.Activity
import android.media.projection.MediaProjectionManager
import com.phonedock.app.capture.ScreenStreamer
import com.phonedock.app.R
import kotlinx.coroutines.*
import java.net.ServerSocket
import java.net.Socket

class ConnectionService : Service() {

    private val serviceScope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    private var serverSocket: ServerSocket? = null
    private var nsdHelper: NsdHelper? = null
    private var screenStreamer: ScreenStreamer? = null
    private var activeClient: Socket? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (intent?.action == ACTION_START_PROJECTION) {
            val resultCode = intent.getIntExtra(EXTRA_PROJECTION_RESULT_CODE, Activity.RESULT_CANCELED)
            val data = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                intent.getParcelableExtra(EXTRA_PROJECTION_DATA, Intent::class.java)
            } else {
                @Suppress("DEPRECATION")
                intent.getParcelableExtra(EXTRA_PROJECTION_DATA)
            }
            if (resultCode == Activity.RESULT_OK && data != null) {
                startProjection(resultCode, data)
            }
        }
        return START_NOT_STICKY
    }

    private fun startProjection(resultCode: Int, data: Intent) {
        val mpManager = getSystemService(MEDIA_PROJECTION_SERVICE) as MediaProjectionManager
        val mediaProjection = mpManager.getMediaProjection(resultCode, data)
        
        val metrics = resources.displayMetrics
        screenStreamer = ScreenStreamer(
            this,
            mediaProjection,
            metrics.widthPixels,
            metrics.heightPixels,
            metrics.densityDpi
        )
        
        screenStreamer?.startStreaming { frameData, pts, isKeyFrame ->
            sendFrame(frameData, isKeyFrame)
        }
    }

    private fun sendFrame(data: ByteArray, isKeyFrame: Boolean) {
        activeClient?.let { socket ->
            serviceScope.launch {
                try {
                    val output = socket.getOutputStream()
                    val header = java.nio.ByteBuffer.allocate(5)
                    header.putInt(data.size)
                    header.put(if (isKeyFrame) 1.toByte() else 0.toByte())

                    synchronized(output) {
                        if (!socket.isClosed && socket.isConnected) {
                            output.write(header.array())
                            output.write(data)
                            output.flush()
                        }
                    }
                } catch (e: Exception) {
                    Log.e(TAG, "Failed to send frame", e)
                }
            }
        }
    }

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
        startForeground(NOTIFICATION_ID, createNotification("Starting server..."))
        
        nsdHelper = NsdHelper(this)
        startServer()
    }

    private fun startServer() {
        serviceScope.launch {
            try {
                serverSocket = ServerSocket(0) // Dynamic port
                val port = serverSocket!!.localPort
                Log.d(TAG, "Server started on port: $port")
                
                nsdHelper?.registerService(port)
                
                updateNotification("Ready for connection on port $port")

                while (isActive) {
                    val clientSocket = serverSocket?.accept()
                    clientSocket?.let {
                        handleClient(it)
                    }
                }
            } catch (e: Exception) {
                Log.e(TAG, "Server error", e)
                stopSelf()
            }
        }
    }

    private fun handleClient(socket: Socket) {
        serviceScope.launch {
            try {
                activeClient = socket
                val clientAddress = socket.inetAddress.hostAddress
                Log.d(TAG, "Client connected: $clientAddress")
                updateNotification("Connected to $clientAddress")
                
                // TODO: Implement Handshake and PDP Protocol
                
                socket.use {
                    // Keep connection alive for now
                    while (isActive && !socket.isClosed) {
                        delay(1000)
                    }
                }
                Log.d(TAG, "Client disconnected")
                activeClient = null
                updateNotification("Waiting for connection...")
            } catch (e: Exception) {
                Log.e(TAG, "Client handling error", e)
            }
        }
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "PhoneDock Connection",
                NotificationManager.IMPORTANCE_LOW
            )
            val manager = getSystemService(NotificationManager::class.java)
            manager.createNotificationChannel(channel)
        }
    }

    private fun createNotification(content: String): Notification {
        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("PhoneDock")
            .setContentText(content)
            .setSmallIcon(R.mipmap.ic_launcher) // TODO: Use proper icon
            .setOngoing(true)
            .build()
    }

    private fun updateNotification(content: String) {
        val manager = getSystemService(NotificationManager::class.java)
        manager.notify(NOTIFICATION_ID, createNotification(content))
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onDestroy() {
        super.onDestroy()
        serviceScope.cancel()
        nsdHelper?.unregisterService()
        serverSocket?.close()
        Log.d(TAG, "Service destroyed")
    }

    companion object {
        private const val TAG = "ConnectionService"
        private const val CHANNEL_ID = "connection_channel"
        private const val NOTIFICATION_ID = 1

        const val ACTION_START_PROJECTION = "com.phonedock.app.ACTION_START_PROJECTION"
        const val EXTRA_PROJECTION_RESULT_CODE = "projection_result_code"
        const val EXTRA_PROJECTION_DATA = "projection_data"
    }
}
