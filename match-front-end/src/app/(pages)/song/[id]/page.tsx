import { Song } from "@/utils/types/song";
import { Suspense } from "react";
import getSong from "@/utils/api/song";
import SongClient from "./SongClient";
import LoadingSpinner from "@/components/common/LoadingSpinner";
import { notFound } from "next/navigation";

const fetchSong = async (id: string): Promise<Song | undefined> => {
  const res = await getSong(id);
  if (!res.ok) {
    return undefined;
  }
  return res.json();
};

const SongPage = async ({ params }: { params: Promise<{ id: string }> }) => {
  const song = await fetchSong((await params).id);

  if (!song) {
    notFound();
  }

  return (
    <Suspense fallback={<LoadingSpinner />}>
      <SongClient song={song} />
    </Suspense>
  );
};

export default SongPage;
