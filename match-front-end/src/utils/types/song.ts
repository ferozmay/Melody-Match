export type Song = {
  id: string;
  title: string;
  artist: string;
  artistId: number;
  runtime: string;
  albumCover: string;
  link: string;
  artistLink: string;
  album: string;
  albumId: number;
  albumLink: string;
  genres: string;
  similarSongs?: Song[];
};
