import { Suspense } from "react";
import { notFound } from "next/navigation";
import { Artist } from "@/utils/types/artist";
import ArtistClient from "./ArtistClient";
import LoadingSpinner from "@/components/common/LoadingSpinner";
import getArtist from "@/utils/api/artist";

async function fetchArtist(id: string): Promise<Artist | undefined> {
  const res = await getArtist(id);
  if (!res.ok) {
    return undefined;
  }
  return res.json();
}

// const ArtistPageComponent =

const ArtistPage = async ({ params }: { params: Promise<{ id: string }> }) => {
  // const { id } = useParams() as { id: string };
  const artist = await fetchArtist((await params).id);

  if (!artist) {
    notFound();
  }

  return (
    <Suspense fallback={<LoadingSpinner />}>
      <ArtistClient artist={artist} />
    </Suspense>
  );
};

export default ArtistPage;
