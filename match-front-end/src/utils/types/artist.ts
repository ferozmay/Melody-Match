import { Album } from "./album";
import { Song } from "./song";

export type Artist = {
  id: number;
  name: string;
  artistImage: string;
  link: string;
  bio: string;
  songs?: Song[];
  albums?: Album[];
};
