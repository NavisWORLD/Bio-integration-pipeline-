import SwiftUI

@MainActor
final class BridgeModel: ObservableObject {
    @Published var endpoint = "http://127.0.0.1:8765"
    @Published var sensor = "ios-app"
    @Published var channel = "heart_rate"
    @Published var value = "72.0"
    @Published var unit = "bpm"
    @Published var quality = "0.98"
    @Published var result = "Ready. Start the COSMOS local bridge and send a measurement."
    @Published var busy = false
    private var sequence = 0

    func demoBeat() {
        let bpm = 72.0 + 4.0 * sin(Double(sequence + 1) / 2.0)
        value = String(format: "%.2f", bpm)
        send()
    }

    func send() {
        guard let numericValue = Double(value), let numericQuality = Double(quality), (0...1).contains(numericQuality) else {
            result = "Value must be numeric and quality must be between 0 and 1."
            return
        }
        guard let url = URL(string: endpoint.trimmingCharacters(in: CharacterSet(charactersIn: "/")) + "/v1/observe") else {
            result = "Bridge endpoint is not a valid URL."
            return
        }
        sequence += 1
        let body: [String: Any] = [
            "sensor": sensor,
            "channel": channel,
            "value": numericValue,
            "unit": unit,
            "quality": numericQuality,
            "sequence": sequence,
            "subject_id": "mobile-user",
            "device_id": "ios-app"
        ]
        busy = true
        result = "Sending observation…"
        Task {
            do {
                var request = URLRequest(url: url)
                request.httpMethod = "POST"
                request.setValue("application/json", forHTTPHeaderField: "Content-Type")
                request.httpBody = try JSONSerialization.data(withJSONObject: body)
                request.timeoutInterval = 8
                let (data, response) = try await URLSession.shared.data(for: request)
                let code = (response as? HTTPURLResponse)?.statusCode ?? 0
                let text = String(data: data, encoding: .utf8) ?? "<binary response>"
                result = "HTTP \(code)\n\n\(text)"
            } catch {
                result = "Connection failed: \(error.localizedDescription)\n\nSimulator default: http://127.0.0.1:8765. A physical iPhone needs the host LAN address and a secured network-facing bridge."
            }
            busy = false
        }
    }
}

struct ContentView: View {
    @StateObject private var model = BridgeModel()

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 16) {
                    VStack(alignment: .leading, spacing: 5) {
                        Text("COSMOS Bio/CNS")
                            .font(.largeTitle.bold())
                        Text("Biosignal → baseline → fusion → 12D CNS")
                            .foregroundStyle(.secondary)
                    }

                    Label("Local-first client. Send only measurements you intend to process.", systemImage: "heart.text.square")
                        .font(.subheadline)
                        .foregroundStyle(.blue)

                    GroupBox("Bridge") {
                        VStack(spacing: 12) {
                            TextField("Endpoint", text: $model.endpoint)
                                .textInputAutocapitalization(.never)
                                .keyboardType(.URL)
                            Divider()
                            TextField("Sensor", text: $model.sensor)
                            Divider()
                            TextField("Channel", text: $model.channel)
                            Divider()
                            HStack {
                                TextField("Value", text: $model.value)
                                    .keyboardType(.decimalPad)
                                TextField("Unit", text: $model.unit)
                            }
                            Divider()
                            TextField("Quality 0..1", text: $model.quality)
                                .keyboardType(.decimalPad)
                        }
                        .textFieldStyle(.plain)
                    }

                    HStack {
                        Button(action: model.send) {
                            Label("Send observation", systemImage: "paperplane.fill")
                                .frame(maxWidth: .infinity)
                        }
                        .buttonStyle(.borderedProminent)
                        .disabled(model.busy)

                        Button("Demo beat", action: model.demoBeat)
                            .buttonStyle(.bordered)
                            .disabled(model.busy)
                    }

                    GroupBox("Response") {
                        ScrollView(.horizontal, showsIndicators: true) {
                            Text(model.result)
                                .font(.system(.footnote, design: .monospaced))
                                .textSelection(.enabled)
                                .frame(maxWidth: .infinity, alignment: .leading)
                        }
                    }
                }
                .padding(20)
            }
            .background(Color(uiColor: .systemGroupedBackground))
        }
    }
}
