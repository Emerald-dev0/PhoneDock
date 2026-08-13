#pragma once

#include <windows.h>
#include <mfapi.h>
#include <mftransform.h>
#include <mfobjects.h>
#include <wrl/client.h>
#include <functional>
#include <vector>

namespace PhoneDock::App {

class VideoDecoder {
public:
    VideoDecoder();
    ~VideoDecoder();

    bool Initialize(ID3D11Device* d3dDevice);
    void Decode(const uint8_t* data, size_t size, std::function<void(ID3D11Texture2D*)> onFrameDecoded);

private:
    Microsoft::WRL::ComPtr<IMFTransform> m_decoderMFT;
    Microsoft::WRL::ComPtr<IMFDXGIDeviceManager> m_deviceManager;
    uint32_t m_resetToken;

    bool ConfigureMediaType();
};

} // namespace PhoneDock::App
