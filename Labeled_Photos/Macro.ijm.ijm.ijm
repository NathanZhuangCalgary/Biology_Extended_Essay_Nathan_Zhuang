// ============================================================
// SEMI-AUTOMATIC LEAF SURFACE AREA MEASUREMENT
// ============================================================
//
// For each image:
//
// 1. Open image
// 2. Convert to 8-bit
// 3. Open Set Scale dialog
// 4. User draws line over ruler and enters known distance
// 5. Open Threshold window with 9-75 pre-entered
// 6. User adjusts threshold
// 7. Apply threshold / convert to mask
// 8. User draws ROI around leaf
// 9. Measure WHITE leaf pixels inside ROI
// 10. Save filename + area
// 11. Close image
// 12. Open next image
//
// ============================================================


// ============================================================
// FOLDERS
// ============================================================

input = "/Users/nathanzhuang/Desktop/Experiment/Labeled_Photos/";
output = "/Users/nathanzhuang/Desktop/Experiment/Results/";


// ============================================================
// CLEAR PREVIOUS RESULTS
// ============================================================

run("Clear Results");


// ============================================================
// PROCESS IMAGES NUMERICALLY
//
// M1_T1_D1
// M1_T1_D2
// ...
// M1_T1_D14
// M1_T2_D1
// ...
// M6_T5_D14
// ============================================================

for (measurement = 1; measurement <= 6; measurement++) {

    for (trial = 1; trial <= 5; trial++) {

        for (day = 1; day <= 14; day++) {


            // ------------------------------------------------
            // CREATE FILENAME
            // ------------------------------------------------

            filename = "M" + measurement + "_T" + trial + "_D" + day + ".JPG";


            // ------------------------------------------------
            // CHECK IF FILE EXISTS
            // ------------------------------------------------

            if (File.exists(input + filename)) {


                // ====================================================
                // OPEN IMAGE
                // ====================================================

                open(input + filename);


                // ====================================================
                // CONVERT TO 8-BIT
                // ====================================================

                run("8-bit");


                // ====================================================
                // SET SCALE
                // ====================================================
                //
                // A line tool will be activated.
                //
                // Draw the line over your ruler.
                // Then the Set Scale dialog will appear.
                //
                // Enter the known distance in cm.
                //
                // Example:
                // Distance in Pixels = 421
                // Known Distance = 1
                // Unit = cm
                //
                // Do NOT check Global.
                // ====================================================

                setTool("line");

                waitForUser(
                    "Set Scale",
                    "Draw a line over the ruler corresponding to a known distance.\n\n" +
                    "Then click OK."
                );

                run("Set Scale...", "known=1 unit=cm");


                // ====================================================
                // THRESHOLD
                // ====================================================
                //
                // Open Threshold with the initial threshold
                // already set to 9-75.
                //
                // Adjust the sliders until the leaf is selected
                // correctly.
                // ====================================================

                setThreshold(9, 75);

                run("Threshold...");


                waitForUser(
                    "Adjust Threshold",
                    "Adjust the threshold until the leaf is selected correctly.\n\n" +
                    "Start from 9-75 and modify it if necessary.\n\n" +
                    "When satisfied, click OK."
                );


                // ====================================================
                // CONVERT TO BINARY MASK
                // ====================================================

                setOption("BlackBackground", true);

                run("Convert to Mask");


                // ====================================================
                // SELECT ROI
                // ====================================================

                setTool("rectangle");

                waitForUser(
                    "Select ROI",
                    "Draw the rectangle around the leaf area you want to measure.\n\n" +
                    "Make sure the entire desired area is inside the ROI,\n" +
                    "then click OK."
                );


                // ====================================================
                // COUNT WHITE LEAF PIXELS
                // ====================================================
                //
                // Binary mask:
                //
                // 0   = black background
                // 255 = white leaf
                //
                // Histogram is calculated only inside the ROI.
                // ====================================================

                getHistogram(values, counts, 256);

                leafPixels = counts[255];


                // ====================================================
                // CALCULATE AREA
                // ====================================================
                //
                // Because Set Scale was manually calibrated for
                // THIS image, ImageJ's pixel-to-cm relationship
                // can be obtained from the calibration.
                //
                // Pixel width and height are retrieved from the
                // current image calibration.
                // ====================================================

                getPixelSize(unit, pixelWidth, pixelHeight, voxelDepth);

                pixelArea = pixelWidth * pixelHeight;

                leafArea = leafPixels * pixelArea;


                // ====================================================
                // SAVE RESULTS
                // ====================================================

                row = nResults;

                setResult("Image", row, filename);
                setResult("Day", row, day);
                setResult("Measurement", row, measurement);
                setResult("Trial", row, trial);
                setResult("Leaf Pixels", row, leafPixels);
                setResult("Area_cm2", row, leafArea);

                updateResults();


                // ====================================================
                // CLOSE IMAGE
                // ====================================================

                close();

            } else {

                print("WARNING: Missing " + filename);

            }
        }
    }
}


// ============================================================
// SAVE RESULTS
// ============================================================

saveAs(
    "Results",
    output + "surface_area_results.csv"
);


// ============================================================
// FINISHED
// ============================================================

print("======================================");
print("Finished processing all images.");
print("Results saved to:");
print(output + "surface_area_results.csv");
print("======================================");