from video_features_extractor_full import extract_all_features

video_path = "example.mp4"
features = extract_all_features(video_path)

print("Frame Difference Mean:", features["frame_diff_mean"][:5])
print("Brightness:", features["brightness"][:5])
print("Blur:", features["blur"][:5])
print("Optical Flow:", features["optical_flow"][:5])
