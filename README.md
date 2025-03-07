<div style="display: flex; align-items: center;">
  <img src="logo.png" alt="Melody Match Logo" style="width: 70px; height: auto; margin-right: 10px;">
  <h1><code>Melody-Match</code></h1>
</div>

Melody Match: Match any vibe with free music!

### GCloud bucket mounting
- Mount: `sudo mount -t gcsfuse -o rw,noauto,user,implicit_dirs,allow_other melody-match-fma /home/plush337/fma-bucket/`
- Unmount: `sudo umount /home/plush337/fma-bucket`
- Before starting nginx, the bucket needs to be mounted