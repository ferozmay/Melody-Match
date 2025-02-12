import { Song } from "./song";

export type Album = {
  id: number;
  title: string;
  artist: string;
  image: string;
  link: string;
  artistLink: string;
  songs: Song[];
  releaseDate: string;
};
