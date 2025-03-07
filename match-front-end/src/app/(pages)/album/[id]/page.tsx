import { Suspense } from "react";
import getAlbum from "@/utils/api/album";
import AlbumClient from "./AlbumClient";
import LoadingSpinner from "@/components/common/LoadingSpinner";
import { notFound } from "next/navigation";
import { Album } from "@/utils/types/album";

const fetchAlbum = async (id: string): Promise<Album | undefined> => {
  const response = await getAlbum(id);
  if (!response.ok) {
    return undefined;
  }
  return response.json();
};

interface AlbumPageProps {
  params: Promise<{ id: string }>;
}

const AlbumPage = async ({ params }: AlbumPageProps) => {
  const album = await fetchAlbum((await params).id);

  if (!album) {
    notFound();
  }

  return (
    <Suspense fallback={<LoadingSpinner />}>
      <AlbumClient album={album} />
    </Suspense>
  );
};

export default AlbumPage;
