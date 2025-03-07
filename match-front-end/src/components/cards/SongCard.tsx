"use client";
import { Song } from "@/utils/types/song";
import Link from "next/link";
import convertRuntime from "@/utils/song/runtime";
import { FaPlay, FaPause } from "react-icons/fa6";
import { playerStore } from "../common/PlayerControls";
import LoadingSpinner from "../common/LoadingSpinner";

const SongCard = ({
  song,
  inline = false,
}: {
  song: Song;
  inline?: boolean;
}) => {
  const runtime = convertRuntime(Number(song.runtime));
  // const { isPlaying, togglePlaying } = useAudioPlayback(song);
  const isPlaying = playerStore((state) => state.isPlaying);
  const togglePlaying = playerStore((state) => state.togglePlaying);
  const setSong = playerStore((state) => state.setCurrentSong);
  const isLoading = playerStore((state) => state.isLoading);
  const currentSong = playerStore((state) => state.currentSong);

  // inline card
  if (true) {
    return (
      <Link
        href={`/song/${song.id}`}
        passHref
        key={song.id}
        className="group select-none cursor-pointer flex items-start p-3 rounded-lg bg-white/10 hover:bg-white/20 hover:shadow-lg backdrop-blur-md transition duration-150 w-full h-[100px]"
      >
        {/* song Cover + play button */}
        <div className="relative my-auto w-20 mr-4">
          <img
            src={song.albumCover || "/images/placeholder.png"}
            onError={(e) => {
              e.currentTarget.src = "/images/placeholder.png";
            }}
            alt={song.title.slice(0, 10)}
            className="rounded-md"
          />
          {/* hoverable play button */}
          <button
            className="w-full h-full absolute top-0 left-0 flex items-center justify-center bg-black/75 rounded-md p-2 opacity-0 group-hover:opacity-100 transition-opacity duration-150"
            onClick={(e) => {
              // e.stopPropagation();
              e.preventDefault();

              if (currentSong?.id !== song.id) {
                setSong(song);
              } else {
                togglePlaying();
              }
            }}
          >
            {isLoading && currentSong?.id === song.id && <LoadingSpinner />}
            {!isLoading && isPlaying && currentSong?.id === song.id ? (
              <FaPause className="text-white text-2xl" />
            ) : (
              <FaPlay className="text-white text-2xl" />
            )}
          </button>
        </div>

        {/* Song Info */}
        <div className="w-full flex flex-col items-start overflow-hidden ">
          <h3 className="w-full text-xl font-bold text-orange-400 hover:text-orange-300 line-clamp-1">
            {song.title}
          </h3>

          <p className="text-gray-200 line-clamp-1">{song.artist}</p>
          <p className="text-gray-400">{runtime}</p>
        </div>

        {/* <div className="absolute left-0 top-0 w-full h-full p-3 bg-black/75 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-150 flex flex-col overflow-y-auto">
          <h3 className="text-xl font-bold text-orange-300">{song.title}</h3>
          <p className="text-sm">{song.artist}</p>
          <p className="text-gray-400 text-sm mt-auto">{runtime}</p>
          <audio
            src={audioUrl | "#"}
            controls
            className="w-full mt-2"
            onPlay={() => setIsPlaying(true)}
            onPause={() => setIsPlaying(false)}
          ></audio>
          <button
            className="bg-orange-400 text-white rounded-lg px-3 py-1 mt-2"
            onClick={(e) => {
              e.stopPropagation();
              setIsPlaying(!isPlaying);
            }}
          >
            {isPlaying ? "Pause" : "Play"}
          </button>
        </div> */}
      </Link>
    );
  }
  if (inline) return;
  // full length card
  // return (
  //   <Link href={`/song/${song.id}`} key={song.id}>
  //     <div className="group select-none cursor-pointer flex items-start p-3 rounded-lg bg-white/10 hover:bg-white/20 hover:shadow-lg backdrop-blur-md transition duration-150">
  //       {/* Album Cover */}
  //       <img
  //         src={song.albumCover}
  //         alt={song.title}
  //         className="h-16 w-16 rounded-[5px] mr-[15px]"
  //         onError={(e) => {
  //           e.currentTarget.src = "/images/placeholder.png";
  //         }}
  //       />

  //       {/* Song Info */}
  //       <div className="w-full flex flex-col items-start">
  //         <h3 className="text-xl font-bold text-orange-400 hover:text-orange-300 line-clamp-2">
  //           {song.title}
  //         </h3>

  //         <p className="line-clamp-1">{song.artist}</p>
  //         <p className="text-gray-400">{runtime}</p>
  //       </div>
  //     </div>
  //   </Link>
  // );
};

export default SongCard;
