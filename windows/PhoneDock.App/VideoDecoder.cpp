#include "VideoDecoder.h"
#include <wmcodecdsp.h>
#include <mferror.h>

#pragma comment(lib, "mfplat.lib")
#pragma comment(lib, "mfuuid.lib")

namespace PhoneDock::App {

VideoDecoder::VideoDecoder() : m_resetToken(0) {
    MFStartup(MF_VERSION);
}

VideoDecoder::~VideoDecoder() {
    MFShutdown();
}

bool VideoDecoder::Initialize(ID3D11Device* d3dDevice) {
    HRESULT hr = CoCreateInstance(CLSID_CMSH264DecoderMFT, nullptr, CLSCTX_INPROC_SERVER, IID_PPV_ARGS(&m_decoderMFT));
    if (FAILED(hr)) return false;

    // Enable Low Latency
    Microsoft::WRL::ComPtr<IMFAttributes> attributes;
    hr = m_decoderMFT->GetAttributes(&attributes);
    if (SUCCEEDED(hr)) {
        attributes->SetUINT32(MF_LOW_LATENCY, TRUE);
    }

    // Set D3D11 Manager for hardware textures
    hr = MFCreateDXGIDeviceManager(&m_resetToken, &m_deviceManager);
    if (FAILED(hr)) return false;

    hr = m_deviceManager->ResetDevice(d3dDevice, m_resetToken);
    if (FAILED(hr)) return false;

    hr = m_decoderMFT->ProcessMessage(MFT_MESSAGE_SET_D3D_MANAGER, reinterpret_cast<ULONG_PTR>(m_deviceManager.Get()));
    if (FAILED(hr)) return false;

    return ConfigureMediaType();
}

bool VideoDecoder::ConfigureMediaType() {
    Microsoft::WRL::ComPtr<IMFMediaType> inputType;
    MFCreateMediaType(&inputType);
    inputType->SetGUID(MF_MT_MAJOR_TYPE, MFMediaType_Video);
    inputType->SetGUID(MF_MT_SUBTYPE, MFVideoFormat_H264);

    HRESULT hr = m_decoderMFT->SetInputType(0, inputType.Get(), 0);
    if (FAILED(hr)) return false;

    Microsoft::WRL::ComPtr<IMFMediaType> outputType;
    MFCreateMediaType(&outputType);
    outputType->SetGUID(MF_MT_MAJOR_TYPE, MFMediaType_Video);
    outputType->SetGUID(MF_MT_SUBTYPE, MFVideoFormat_NV12); // Hardware decoding usually outputs NV12

    hr = m_decoderMFT->SetOutputType(0, outputType.Get(), 0);
    return SUCCEEDED(hr);
}

void VideoDecoder::Decode(const uint8_t* data, size_t size, std::function<void(ID3D11Texture2D*)> onFrameDecoded) {
    // TODO: Implement ProcessInput and ProcessOutput loop
}

} // namespace PhoneDock::App
