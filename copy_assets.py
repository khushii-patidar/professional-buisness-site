import os
import shutil

src_dir = r"C:\Users\Ambika\.gemini\antigravity\brain\22e7b667-f30e-421f-b916-5ffa7809c43d\.user_uploaded"
dest_dir = r"c:\Users\Ambika\Downloads\Lokeshh_Ai_Tools_GreenCream_Professional (1)\editor_lokesh\portfolio\static\images"

os.makedirs(dest_dir, exist_ok=True)

# Copy profile photo
profile_src = os.path.join(src_dir, "media_1787731791265.jpg")
profile_dest = os.path.join(dest_dir, "lokesh_profile.jpg")
if os.path.exists(profile_src):
    shutil.copyfile(profile_src, profile_dest)
    print("Copied profile photo to:", profile_dest)

# Copy scanner QR
qr_src = os.path.join(src_dir, "media_1787731682886.png")
qr_dest = os.path.join(dest_dir, "payment_qr.png")
if os.path.exists(qr_src):
    shutil.copyfile(qr_src, qr_dest)
    print("Copied QR scanner to:", qr_dest)

print("Done copying assets!")
