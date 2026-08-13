#include <iostream>
#include <thread>
#include "Discovery.h"
#include "SessionClient.h"
#include "VideoDecoder.h"
#include "Renderer.h"

int main() {
    std::wcout << L"PhoneDock Windows Discovery Agent starting..." << std::endl;

    PhoneDock::App::DiscoveryAgent discovery;
    PhoneDock::App::SessionClient client;
    PhoneDock::App::VideoDecoder decoder;
    PhoneDock::App::Renderer renderer;

    discovery.StartBrowsing([&](const PhoneDock::App::DiscoveredService& service) {
        std::wcout << L"Found PhoneDock Device: " << service.instanceName << std::endl;

        // Auto-connect to the first device found for testing
        if (client.Connect(service.ipAddress, service.port)) {
            std::cout << "Connected to phone!" << std::endl;

            renderer.Initialize(1080, 1920); // TODO: Get actual dimensions
            decoder.Initialize(renderer.GetDevice());

            client.StartListening([&](const std::vector<uint8_t>& data, bool isKeyFrame) {
                decoder.Decode(data.data(), data.size(), [&](ID3D11Texture2D* texture) {
                    renderer.Present(texture);
                });
            });
        }
    });

    std::cout << "Press Enter to exit..." << std::endl;
    std::cin.get();

    client.Disconnect();
    discovery.StopBrowsing();

    return 0;
}
