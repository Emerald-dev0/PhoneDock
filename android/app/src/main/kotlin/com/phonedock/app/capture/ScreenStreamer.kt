package com.phonedock.app.capture

import android.content.Context
import android.hardware.display.DisplayManager
import android.hardware.display.VirtualDisplay
import android.media.MediaCodec
import android.media.MediaCodecInfo
import android.media.MediaFormat
import android.media.projection.MediaProjection
import android.util.Log
import android.view.Surface
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import java.nio.ByteBuffer

class ScreenStreamer(
    private val context: Context,
    private val mediaProjection: MediaProjection,
    private val width: Int,
    private val height: Int,
    private val densityDpi: Int
) {
    private var encoder: MediaCodec? = null
    private var virtualDisplay: VirtualDisplay? = null
    private var streamingJob: Job? = null
    private val scope = CoroutineScope(Dispatchers.IO)

    fun startStreaming(onFrameEncoded: (ByteArray, Long, Boolean) -> Unit) {
        val format = MediaFormat.createVideoFormat(MediaFormat.MIMETYPE_VIDEO_AVC, width, height)
        format.setInteger(MediaFormat.KEY_COLOR_FORMAT, MediaCodecInfo.CodecCapabilities.COLOR_FormatSurface)
        format.setInteger(MediaFormat.KEY_BIT_RATE, 4000000) // 4Mbps
        format.setInteger(MediaFormat.KEY_FRAME_RATE, 60)
        format.setInteger(MediaFormat.KEY_I_FRAME_INTERVAL, 1) // 1 second between keyframes
        
        // Low latency settings
        format.setInteger(MediaFormat.KEY_LATENCY, 0)
        format.setInteger(MediaFormat.KEY_PRIORITY, 0) // Real-time

        encoder = MediaCodec.createEncoderByType(MediaFormat.MIMETYPE_VIDEO_AVC)
        encoder?.configure(format, null, null, MediaCodec.CONFIGURE_FLAG_ENCODE)
        
        val inputSurface = encoder?.createInputSurface() ?: return
        
        virtualDisplay = mediaProjection.createVirtualDisplay(
            "PhoneDockCapture",
            width,
            height,
            densityDpi,
            DisplayManager.VIRTUAL_DISPLAY_FLAG_AUTO_MIRROR,
            inputSurface,
            null,
            null
        )

        encoder?.start()

        streamingJob = scope.launch {
            val bufferInfo = MediaCodec.BufferInfo()
            while (isActive) {
                val outputBufferId = encoder?.dequeueOutputBuffer(bufferInfo, 10000) ?: -1
                if (outputBufferId >= 0) {
                    val outputBuffer = encoder?.getOutputBuffer(outputBufferId)
                    if (outputBuffer != null) {
                        val data = ByteArray(bufferInfo.size)
                        outputBuffer.get(data)
                        
                        val isKeyFrame = (bufferInfo.flags and MediaCodec.BUFFER_FLAG_KEY_FRAME) != 0
                        onFrameEncoded(data, bufferInfo.presentationTimeUs, isKeyFrame)
                        
                        encoder?.releaseOutputBuffer(outputBufferId, false)
                    }
                }
            }
        }
    }

    fun stopStreaming() {
        streamingJob?.cancel()
        streamingJob = null
        
        virtualDisplay?.release()
        virtualDisplay = null
        
        encoder?.stop()
        encoder?.release()
        encoder = null
    }

    companion object {
        private const val TAG = "ScreenStreamer"
    }
}
