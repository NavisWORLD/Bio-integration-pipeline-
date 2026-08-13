package world.navis.cosmosbiocns;

import android.app.Activity;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.os.Bundle;
import android.text.InputType;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Locale;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class MainActivity extends Activity {
    private final ExecutorService executor = Executors.newSingleThreadExecutor();
    private EditText endpoint;
    private EditText sensor;
    private EditText channel;
    private EditText value;
    private EditText unit;
    private EditText quality;
    private TextView output;
    private int sequence = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(buildUi());
    }

    private View buildUi() {
        ScrollView scroll = new ScrollView(this);
        scroll.setBackgroundColor(Color.rgb(244, 247, 251));
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(dp(20), dp(24), dp(20), dp(32));
        scroll.addView(root);

        TextView title = label("COSMOS Bio/CNS", 28, true);
        root.addView(title);
        TextView subtitle = label("Biosignal → baseline → fusion → 12D CNS", 15, false);
        subtitle.setTextColor(Color.rgb(75, 86, 101));
        root.addView(subtitle, marginTop(4));

        TextView privacy = label("Local-first client. Send only measurements you intend to process.", 13, false);
        privacy.setTextColor(Color.rgb(49, 92, 155));
        root.addView(privacy, marginTop(14));

        endpoint = field("Bridge endpoint", "http://10.0.2.2:8765");
        sensor = field("Sensor", "android-app");
        channel = field("Channel", "heart_rate");
        value = field("Value", "72.0");
        value.setInputType(InputType.TYPE_CLASS_NUMBER | InputType.TYPE_NUMBER_FLAG_DECIMAL | InputType.TYPE_NUMBER_FLAG_SIGNED);
        unit = field("Unit", "bpm");
        quality = field("Quality 0..1", "0.98");
        quality.setInputType(InputType.TYPE_CLASS_NUMBER | InputType.TYPE_NUMBER_FLAG_DECIMAL);

        root.addView(endpoint, marginTop(18));
        root.addView(sensor, marginTop(10));
        root.addView(channel, marginTop(10));
        root.addView(value, marginTop(10));
        root.addView(unit, marginTop(10));
        root.addView(quality, marginTop(10));

        LinearLayout actions = new LinearLayout(this);
        actions.setOrientation(LinearLayout.HORIZONTAL);
        Button send = button("Send observation");
        send.setOnClickListener(v -> sendObservation());
        actions.addView(send, new LinearLayout.LayoutParams(0, dp(48), 1f));
        Button demo = button("Demo beat");
        demo.setOnClickListener(v -> {
            double bpm = 72.0 + 4.0 * Math.sin((sequence + 1) / 2.0);
            value.setText(String.format(Locale.US, "%.2f", bpm));
            sendObservation();
        });
        LinearLayout.LayoutParams demoParams = new LinearLayout.LayoutParams(0, dp(48), 0.7f);
        demoParams.leftMargin = dp(8);
        actions.addView(demo, demoParams);
        root.addView(actions, marginTop(16));

        output = label("Ready. Start the local bridge, then send a measurement.", 14, false);
        output.setTextIsSelectable(true);
        output.setPadding(dp(16), dp(16), dp(16), dp(16));
        output.setBackground(card(Color.WHITE));
        root.addView(output, marginTop(18));
        return scroll;
    }

    private void sendObservation() {
        final String base = endpoint.getText().toString().trim().replaceAll("/+$", "");
        final double numericValue;
        final double numericQuality;
        try {
            numericValue = Double.parseDouble(value.getText().toString().trim());
            numericQuality = Double.parseDouble(quality.getText().toString().trim());
            if (numericQuality < 0.0 || numericQuality > 1.0) throw new NumberFormatException();
        } catch (NumberFormatException ex) {
            output.setText("Value must be numeric and quality must be between 0 and 1.");
            return;
        }

        sequence += 1;
        final int seq = sequence;
        output.setText("Sending observation…");
        executor.execute(() -> {
            try {
                JSONObject body = new JSONObject();
                body.put("sensor", sensor.getText().toString().trim());
                body.put("channel", channel.getText().toString().trim());
                body.put("value", numericValue);
                body.put("unit", unit.getText().toString().trim());
                body.put("quality", numericQuality);
                body.put("sequence", seq);
                body.put("subject_id", "mobile-user");
                body.put("device_id", "android-app");

                URL url = new URL(base + "/v1/observe");
                HttpURLConnection connection = (HttpURLConnection) url.openConnection();
                connection.setConnectTimeout(5000);
                connection.setReadTimeout(8000);
                connection.setRequestMethod("POST");
                connection.setRequestProperty("Content-Type", "application/json");
                connection.setDoOutput(true);
                byte[] bytes = body.toString().getBytes(StandardCharsets.UTF_8);
                try (OutputStream stream = connection.getOutputStream()) {
                    stream.write(bytes);
                }
                int code = connection.getResponseCode();
                BufferedReader reader = new BufferedReader(new InputStreamReader(
                        code >= 200 && code < 300 ? connection.getInputStream() : connection.getErrorStream(),
                        StandardCharsets.UTF_8));
                StringBuilder response = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) response.append(line).append('\n');
                reader.close();
                String message = "HTTP " + code + "\n\n" + response;
                runOnUiThread(() -> output.setText(message));
            } catch (Exception ex) {
                runOnUiThread(() -> output.setText(
                        "Connection failed: " + ex.getMessage() +
                        "\n\nAndroid emulator → desktop host default: http://10.0.2.2:8765\n" +
                        "Physical devices need the host LAN address and an appropriately secured bridge."));
            }
        });
    }

    private EditText field(String hint, String initial) {
        EditText input = new EditText(this);
        input.setHint(hint);
        input.setText(initial);
        input.setTextSize(16);
        input.setSingleLine(true);
        input.setPadding(dp(14), 0, dp(14), 0);
        input.setBackground(card(Color.WHITE));
        return input;
    }

    private Button button(String text) {
        Button b = new Button(this);
        b.setText(text);
        b.setTextSize(14);
        return b;
    }

    private TextView label(String text, int size, boolean bold) {
        TextView view = new TextView(this);
        view.setText(text);
        view.setTextSize(size);
        view.setTextColor(Color.rgb(24, 31, 43));
        if (bold) view.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        return view;
    }

    private GradientDrawable card(int color) {
        GradientDrawable drawable = new GradientDrawable();
        drawable.setColor(color);
        drawable.setCornerRadius(dp(12));
        drawable.setStroke(dp(1), Color.rgb(220, 226, 235));
        return drawable;
    }

    private LinearLayout.LayoutParams marginTop(int value) {
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT);
        params.topMargin = dp(value);
        return params;
    }

    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }

    @Override
    protected void onDestroy() {
        executor.shutdownNow();
        super.onDestroy();
    }
}
