import { Song } from "./song";

export type Album = {
  id: number;
  title: string;
  artist: string;
  albumCover: string;
  link: string;
  artistLink: string;
  songs: Song[];
  releaseDate: string;
  genres: string;
};
