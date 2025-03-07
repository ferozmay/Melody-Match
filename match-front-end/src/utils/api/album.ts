import { ALBUMS_URL } from "./const";

const getAlbum = async (album_id: string): Promise<Response> =>
  fetch(ALBUMS_URL + `/${album_id}`);

export default getAlbum;
