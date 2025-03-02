import YouTube, { YouTubePlayer } from "react-youtube";
import { FaPause, FaPlay } from "react-icons/fa6";
import { create } from "zustand";
import { Song } from "@/utils/types/song";
import { AUDIO_URL } from "@/utils/api/const";
import { getYouTubeID } from "@/utils/api/song";
import { useEffect } from "react";
import convertRuntime from "@/utils/song/runtime";
import { ImSpinner2 } from "react-icons/im";

interface PlayerStoreProps {
  audio: HTMLAudioElement | null;
  isPlaying: boolean;
  currentTime: number;
  duration: number;
  isLoading: boolean;
  updateTime: () => void;
  youtubeID: string | null;
  youtubeRef: YouTubePlayer | null;
  pendingYTplay: boolean;
  setPendingYTplay: (pending: boolean) => void;
  setYTRef: (ref: YouTubePlayer) => void;
  currentSong: Song | null;
  setCurrentSong: (song: Song, set_play?: boolean) => void;
  togglePlaying: () => void;
  setPlaying: (playing: boolean) => void;
  play: () => void;
  pause: () => void;
}

const isFMA = (str: string) => {
  // isNumeric
  return /^[0-9]+$/.test(str);
};

export const playerStore = create<PlayerStoreProps>((set, get) => ({
  audio: null,
  isPlaying: false,
  pendingYTplay: false,
  isLoading: false,
  setPendingYTplay: (pending: boolean) => set({ pendingYTplay: pending }),
  currentTime: 0,
  duration: 0,
  updateTime: () => {
    const { audio, youtubeRef, youtubeID } = get();
    if (youtubeRef && youtubeID) {
      set({ currentTime: youtubeRef.getCurrentTime() || 0 });
      set({ duration: youtubeRef.getDuration() || 0 });
      //   youtubeRef.getCurrentTime().then((time) => {
      //   });
      //   youtubeRef.getDuration().then((time) => {
      //   });
    } else {
      set({ currentTime: audio?.currentTime || 0 });
      set({ duration: audio?.duration || 0 });
    }
  },
  youtubeID: null,
  youtubeRef: null,
  currentSong: null,
  setYTRef: (ref: YouTubePlayer) => set({ youtubeRef: ref }),
  setCurrentSong: (song: Song, set_play: boolean = true) => {
    const { audio, play } = get();

    if (audio) {
      audio.pause();
      audio.removeEventListener("play", () => {});
      audio.removeEventListener("pause", () => {});
      audio.removeEventListener("ended", () => {});
    }
    // check fma or msd
    set({ currentSong: song });
    set({ isPlaying: false });
    if (isFMA(song.id)) {
      set({ youtubeID: null });
      const audioFolder = Math.floor(Number(song.id) / 1000)
        .toString()
        .padStart(3, "0");
      const audioPath = song.id.toString().padStart(6, "0");
      const audio = new Audio();
      audio.src = `${AUDIO_URL}/${audioFolder}/${audioPath}.mp3`;
      audio.addEventListener("play", () => set({ isPlaying: true }));
      audio.addEventListener("pause", () => set({ isPlaying: false }));
      audio.addEventListener("ended", () => set({ isPlaying: false }));
      audio.load();
      set({ audio });
      if (set_play) play();
    } else {
      // MSD
      set({ audio: null });
      set({ isLoading: true });
      set({ pendingYTplay: set_play });
      // fetch youtube id
      getYouTubeID(song.id).then((data) => {
        set({ youtubeID: data.youtube_id });
      });
    }
  },
  setPlaying: (playing: boolean) => {
    set({ isPlaying: playing });
  },
  play: () => {
    const { audio, youtubeRef, youtubeID } = get();
    if (audio) {
      if (audio.paused) {
        audio
          .play()
          .then(() => {
            set({ isPlaying: true });
          })
          .catch((e) => {
            console.log("Error playing audio", e);
            set({ isPlaying: false });
          });
      }
    } else if (youtubeRef && youtubeID) {
      youtubeRef.playVideo();
    }
    set({ isLoading: false });
  },
  pause: () => {
    const { audio, youtubeRef } = get();
    if (audio) {
      if (!audio.paused) {
        audio.pause();
        set({ isPlaying: false });
      }
    } else if (youtubeRef) {
      youtubeRef.pauseVideo();
    }
  },
  togglePlaying: () => {
    const { isPlaying, play, pause } = get();
    if (isPlaying) pause();
    else play();
  },
}));

const PlayerControls = () => {
  const isLoading = playerStore((state) => state.isLoading);
  //
  const youtubeID = playerStore((state) => state.youtubeID);
  const setYTRef = playerStore((state) => state.setYTRef);
  const pendingYTplay = playerStore((state) => state.pendingYTplay);
  const setPendingYTplay = playerStore((state) => state.setPendingYTplay);
  //
  const isPlaying = playerStore((state) => state.isPlaying);
  const setPlaying = playerStore((state) => state.setPlaying);
  const togglePlaying = playerStore((state) => state.togglePlaying);
  const play = playerStore((state) => state.play);
  //
  const currentSong = playerStore((state) => state.currentSong);
  const currentTime = playerStore((state) => state.currentTime);
  const duration = playerStore((state) => state.duration);
  const updateTime = playerStore((state) => state.updateTime);

  // update time
  useEffect(() => {
    let intervalId: number | null = null;
    if (isPlaying) {
      intervalId = window.setInterval(updateTime, 500);
    } else if (intervalId) {
      clearInterval(intervalId);
      intervalId = null;
    }
    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [isPlaying, updateTime]);

  return (
    <div className="z-10 px-4 py-2 fixed w-[700px] inset-x-0 mx-auto bottom-12 center bg-white bg-opacity-95 text-black rounded-lg shadow-lg transition duration-150 hover:shadow-2xl gap-4 flex items-center">
      <div className="hidden">
        <YouTube
          videoId={youtubeID || ""}
          //   videoId={"z4PKzz81m5c"}
          // ref={ytRef}
          opts={{
            height: "100",
            width: "100",
            playerVars: {
              autoplay: 0,
            },
          }}
          onReady={(e) => {
            setYTRef(e.target);

            if (pendingYTplay) {
              setTimeout(() => {
                play();
                setPendingYTplay(false);
              }, 1000);
            }
          }}
          onStateChange={(e) => {
            const state = e.target.getPlayerState();
            if (state === 1) {
              setPlaying(true);
            }
            if (state === 2) {
              setPlaying(false);
            }
          }}
        />
      </div>

      <button
        className="py-3 px-3 hover:bg-gray-400/50 h-full w-fit rounded-lg"
        onClick={() => togglePlaying()}
      >
        {isLoading && (
          <div className="animate-spin">
            <ImSpinner2 className="text-4xl" />
          </div>
        )}
        {!isLoading &&
          (isPlaying ? (
            <FaPause className="text-4xl" />
          ) : (
            <FaPlay className="text-4xl" />
          ))}
      </button>
      <div className="time flex flex-col w-full">
        <p className="text-2xl      hover:text-blue-500 cursor-pointer">
          {currentSong?.title || "No Song Playing"}
        </p>
        <p className="text-md -mt-2 hover:text-blue-500 cursor-pointer">
          {currentSong?.artist || "No Artist"}
        </p>
        <span className="h-2 w-full bg-blue-500 rounded"></span>
        <div className="flex text-md justify-between">
          <span>{convertRuntime(currentTime) || 0}</span>
          <span>{convertRuntime(duration) || 0}</span>
        </div>
      </div>
    </div>
  );
};

export default PlayerControls;
