import { useEffect, useState } from "react";
import { Song } from "../types/song";

const useAudioPlayback = (song: Song | null) => {
  const [audioUrl, setAudioUrl] = useState<string>("");
  const [isPlaying, setIsPlaying] = useState(false);
  const [audio, setAudio] = useState<HTMLAudioElement | null>(null);

  useEffect(() => {
    // Clean up previous audio instance
    if (audio) {
      audio.pause();
      audio.src = "";
    }

    // Only create new audio instance if song exists and has preview URL
    if (song?.id) {
      const audioFolder = Math.floor(Number(song.id) / 1000)
        .toString()
        .padStart(3, "0");
      const audioPath = song.id.toString().padStart(6, "0");
      setAudioUrl(`http://35.197.212.29/audio/${audioFolder}/${audioPath}.mp3`);
      const newAudio = new Audio();
      newAudio.src = `http://35.197.212.29/audio/${audioFolder}/${audioPath}.mp3`;
      newAudio.load();
      setAudio(newAudio);
    } else {
      setAudioUrl("");
      setIsPlaying(false);
    }

    // Cleanup function
    return () => {
      if (audio) {
        audio.pause();
        audio.src = "";
      }
    };
  }, [song]);

  const togglePlaying = () => {
    if (audioUrl && audio) {
      if (isPlaying) {
        audio.pause();
      } else {
        audio.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  return { audioUrl, isPlaying, togglePlaying };
};

export default useAudioPlayback;
