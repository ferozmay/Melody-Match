import { create } from "zustand";

export interface PaginatorStoreProps {
  activePage: number;
  setActivePage: (page: number) => void;
}

const paginatorStore = create<PaginatorStoreProps>((set) => ({
  activePage: 1,
  setActivePage: (page: number) => set({ activePage: page }),
}));

export default paginatorStore;
