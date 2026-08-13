#include "Renderer.h"

#pragma comment(lib, "d3d11.lib")
#pragma comment(lib, "dxgi.lib")

namespace PhoneDock::App {

Renderer::Renderer() {}
Renderer::~Renderer() {}

bool Renderer::Initialize(uint32_t width, uint32_t height) {
    UINT creationFlags = D3D11_CREATE_DEVICE_VIDEO_SUPPORT | D3D11_CREATE_DEVICE_BGRA_SUPPORT;
#ifdef _DEBUG
    creationFlags |= D3D11_CREATE_DEVICE_DEBUG;
#endif

    D3D_FEATURE_LEVEL featureLevels[] = { D3D_FEATURE_LEVEL_11_1 };

    HRESULT hr = D3D11CreateDevice(
        nullptr,
        D3D_DRIVER_TYPE_HARDWARE,
        nullptr,
        creationFlags,
        featureLevels,
        ARRAYSIZE(featureLevels),
        D3D11_SDK_VERSION,
        &m_d3dDevice,
        nullptr,
        &m_d3dContext
    );

    if (FAILED(hr)) return false;

    // Query for Video Device
    hr = m_d3dDevice.As(&m_videoDevice);
    if (FAILED(hr)) return false;

    hr = m_d3dContext.As(&m_videoContext);
    if (FAILED(hr)) return false;

    return true;
}

void Renderer::Present(ID3D11Texture2D* texture) {
    // TODO: Implement NV12 -> BGRA conversion and SwapChain Present
}

} // namespace PhoneDock::App
