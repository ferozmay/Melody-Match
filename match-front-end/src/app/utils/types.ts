export type Song = {
    id: number;
    title: string;
    artist: string;
    runtime: string;
    albumCover: string;
    link: string;
}

export type Album = {
    id: number;
    title: string;
    artist: string;
    releaseDate: string;
    albumCover: string;
    noOfTracks: number;
    link: string;
}