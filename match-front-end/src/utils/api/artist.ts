import { ARTISTS_URL } from "./const";

const getArtist = async (artistId: string): Promise<Response> =>
  fetch(ARTISTS_URL + `/${artistId}`);

export default getArtist;
