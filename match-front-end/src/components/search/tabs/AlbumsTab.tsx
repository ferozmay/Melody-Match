import AlbumCard from "@/components/cards/AlbumCard";
import { Album } from "@/utils/types/album";

const AlbumsTab = ({ results }: { results: Album[] }) => {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4">
      {results.map((album: Album, idx: number) => (
        <AlbumCard key={`album-${idx}-${album.id}`} album={album} />
      ))}
    </div>
  );
};

export default AlbumsTab;
