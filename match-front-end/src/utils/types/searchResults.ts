import { Album } from "./album";
import { Artist } from "./artist";
import { Song } from "./song";

export type SearchResults = {
  songs: Song[];
  artists: Artist[];
  albums: Album[];

  track_pages: number;
  artist_pages: number;
  album_pages: number;
};
