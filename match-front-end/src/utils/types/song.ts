export type Song = {
  id: number;
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
  topGenre: string;
  similarSongs?: Song[];
};
