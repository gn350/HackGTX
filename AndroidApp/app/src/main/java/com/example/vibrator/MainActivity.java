package com.example.vibrator;


import android.content.Context;
import android.os.Bundle;
import android.os.VibrationEffect;
import android.os.Vibrator;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.View;
import android.os.Handler;
import android.speech.tts.TextToSpeech;
import android.widget.TextView;
import android.view.MotionEvent;
import android.widget.Toast;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;


import androidx.appcompat.app.AppCompatActivity;

import java.util.ArrayList;
import java.util.Locale;
import java.util.concurrent.atomic.AtomicReference;

public class MainActivity extends AppCompatActivity {

    private boolean vibrating = false;
    private Handler handler;
    private Runnable currentVibrationRunnable;

    private TextToSpeech textToSpeech;

    private Vibrator vibrator;

    private String description;

    private TextView textView;

    private int screenHeight;
    private int screenWidth;

    // Input values
    private int[] data = new int[3]; // the data to be read in

    public String dogImageUrl;

    public void request() {
        RequestQueue volleyQueue = Volley.newRequestQueue(MainActivity.this);
        //String url2 = "http://192.168.122.1:8000/";
        String url = "http://192.168.205.144:8000/";

        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(
                // we are using GET HTTP request method
                Request.Method.GET,
                // url we want to send the HTTP request to
                url,
                // this parameter is used to send a JSON object to the
                // server, since this is not required in our case,
                // we are keeping it `null`
                null,

                // lambda function for handling the case
                // when the HTTP request succeeds
                (Response.Listener<JSONObject>) response -> {
                    // get the image url from the JSON object
                    try {
                        dogImageUrl = response.getString("detection");
                        birdImageUrl = response.getString("item");
                        // load the image into the ImageView using Glide.
                        //System.out.println(dogImageUrl.get());
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                },

                (Response.ErrorListener) error -> {
                    // make a Toast telling the user
                    // that something went wrong
                    Toast.makeText(MainActivity.this, "Some error occurred! Cannot fetch dog image", Toast.LENGTH_LONG).show();
                    // log the error message in the error stream
                    Log.e("MainActivity", error.toString());
                }
        );

        volleyQueue.add(jsonObjectRequest);
        String actualValue;
        //ArrayList<Integer> array = new ArrayList<>();
        //array.add((int) dogImageUrl.charAt(1));
        //array.add((int) dogImageUrl.charAt(3));
        //array.add((int) dogImageUrl.charAt(5));
        //System.out.println(array);
    }
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);  // Ensure this is your correct layout file.

        data[0] = 0;
        data[1] = 1;
        data[2] = 2;

        handler = new Handler();
        vibrator = (Vibrator) getSystemService(Context.VIBRATOR_SERVICE);

        DisplayMetrics displayMetrics = new DisplayMetrics();
        getWindowManager().getDefaultDisplay().getMetrics(displayMetrics);
        screenHeight = displayMetrics.heightPixels;
        screenWidth = displayMetrics.widthPixels;

        textToSpeech = new TextToSpeech(this, new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status == TextToSpeech.SUCCESS) {
                    int langResult = textToSpeech.setLanguage(Locale.US);
                    if (langResult == TextToSpeech.LANG_MISSING_DATA |
                            langResult == TextToSpeech.LANG_NOT_SUPPORTED) {
                        Log.e("TextToSpeech", "Language is not supported or missing data");
                    } else {
                        // Ready to use
                        describeObject("The object is a red ball on the left");
                    }
                } else {
                    Log.e("TextToSpeech", "Initialization failed");
                }
            }
        });

        // Set an onTouchListener on the view
        View view = findViewById(R.id.coordinatorLayout);  // Replace with your view ID
        view.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                // Get the action type
                request();

                data[0] = (int) dogImageUrl.charAt(1);
                data[1] = (int) dogImageUrl.charAt(3);
                data[2] = (int) dogImageUrl.charAt(5);

                float x = event.getX();
                float y = event.getY();

                switch (event.getAction()) {
                    case MotionEvent.ACTION_DOWN:
                        // Finger touches the screen
                        Log.d("TapEvent", "onTouch: ACTION DOWN");
                        describeObject("Garlic");
                        handleTouch(x, y);
                        break;
                    case MotionEvent.ACTION_MOVE:
                        // Finger moves on the screen
                        Log.d("TapEvent", "onTouch: ACTION MOVE");
                        handleTouch(x, y);
                        break;
                    case MotionEvent.ACTION_UP:
                        // Finger leaves the screen
                        Log.d("TapEvent", "onTouch: ACTION UP");
                        handler.removeCallbacks(currentVibrationRunnable);
                        vibrating = false;
                        break;

                    // Return true to indicate that the event has been handled
                }
                return true;
            }
        });
    }

    private void handleTouch(float x, float y) {
        // this will say what the object is
        VibrateRunnable vibrationRunnable = null;

        if (x >= 0 && x < (screenWidth / 3.0)) { // left
            vibrationRunnable = new VibrateRunnable(data[0]);
        } else if (x >= screenWidth / 3.0 && x < 2 * screenWidth / 3.0) { // center
            vibrationRunnable = new VibrateRunnable(data[1]);
        } else if (x >= 2 * screenWidth / 3.0 && x < screenWidth) { // right
            vibrationRunnable = new VibrateRunnable(data[2]);
        }
        if (currentVibrationRunnable == null) {
            currentVibrationRunnable = vibrationRunnable;
        }
        if (vibrationRunnable != null && !currentVibrationRunnable.equals(vibrationRunnable)) {
            handler.removeCallbacks(currentVibrationRunnable);
            vibrating = false;
            currentVibrationRunnable = vibrationRunnable;
            handler.post(currentVibrationRunnable);
            vibrating = true;
        }
    }

    // Method to describe objects using TextToSpeech
    private void describeObject(String description) {
        int speechStatus = textToSpeech.speak(description, TextToSpeech.QUEUE_FLUSH, null, null);

        if (speechStatus == TextToSpeech.ERROR) {
            Log.e("TextToSpeech", "Error in converting Text to Speech!");
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        // Shutdown TextToSpeech
        if (textToSpeech != null) {
            textToSpeech.stop();
            textToSpeech.shutdown();
        }

        if (vibrator != null) {
            vibrator.cancel();
        }
    }

    private void startVibrationSequence() {
        Vibrator vibrator = (Vibrator) getSystemService(Context.VIBRATOR_SERVICE);

        // Check if the device has a vibrator
        if (vibrator != null && vibrator.hasVibrator()) {
            // Define the pattern, like {delay, vibrate, delay, vibrate, ...}
            // Here, 0 means start immediately, 400 means vibrate for 400ms, 200 means pause for 200ms, etc.
            long[] timings = {100, 100, 100};
            int[] amplitudes = {100 * data[0], 100 * data[1], 100 * data[2]};
            long[] pattern = {0, amplitudes[0], 100, amplitudes[1], 100, amplitudes[2]};

            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                // For API level 26 and above
                VibrationEffect effect = VibrationEffect.createWaveform(timings, amplitudes, -1);  // -1 means do not repeat
                vibrator.vibrate(effect);
            } else {
                // For API level 25 and below
                vibrator.vibrate(pattern, -1);  // -1 means do not repeat
            }
        }
    }

    private void handleVibrationClick(Runnable vibrationRunnable) {
        if (vibrating) {
            handler.removeCallbacks(currentVibrationRunnable);
        } else {
            currentVibrationRunnable = vibrationRunnable;
            handler.post(currentVibrationRunnable);
        }
        vibrating = !vibrating;
    }

    class VibrateRunnable implements Runnable {
        int distance; // 0, 1, or 2
                        // 0: no object
                        // 1: far object
                        // 2: close object
        int delayMs;

        VibrateRunnable(int distancia) {
            distance = distancia;
            delayMs = 500;
        }

        @Override
        public void run() {
            // Vibrates the phone with varying intensity based on distance
            Vibrator vibrator = (Vibrator) getSystemService(Context.VIBRATOR_SERVICE);

            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.R) {
                VibrationEffect effect = null;
                if (distance == 1) {
                    effect = VibrationEffect.createPredefined(VibrationEffect.EFFECT_HEAVY_CLICK);
                    delayMs = 500;
                } else if (distance == 2) {
                    effect = VibrationEffect.createPredefined(VibrationEffect.EFFECT_HEAVY_CLICK);
                    delayMs = 50;
                } else if (distance == 0) {
                    effect = VibrationEffect.createPredefined(VibrationEffect.EFFECT_CLICK);
                    delayMs = 850;
                }
                if (effect != null) {
                    vibrator.vibrate(effect);
                }

            } else { // this is if the device doensn't support haptic feedback
                vibrator.vibrate(delayMs);
            }
            // Repeat the vibration after a delay of 500 milliseconds
            handler.postDelayed(this, delayMs);
        }

        @Override
        public boolean equals(Object obj) {
            if (this == obj) {
                return true;
            }
            if (obj == null || getClass() != obj.getClass()) {
                return false;
            }
            VibrateRunnable that = (VibrateRunnable) obj;
            return distance == that.distance;
        }
    }
}