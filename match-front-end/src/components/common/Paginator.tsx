import paginatorStore, { PaginatorStoreProps } from "@/utils/store/paginator";
import React from "react";

const TabButton = ({ number, active }: { number: number; active: boolean }) => {
  const setActivePage = paginatorStore(
    (state: PaginatorStoreProps) => state.setActivePage
  );
  return (
    <button
      onClick={() => setActivePage(number)}
      className={`text-3xl px-4 py-2 rounded-lg border shadow-lg hover:bg-white/50 ${
        active && "bg-white/50"
      } duration-150`}
    >
      {number}
    </button>
  );
};

const Paginator = ({ totalPages }: { totalPages: number }) => {
  const activePage = paginatorStore(
    (state: PaginatorStoreProps) => state.activePage
  );

  return (
    <div className="w-full flex gap-4 justify-center items-center">
      <TabButton number={1} active={activePage === 1} />
      {activePage > 2 && (
        <>
          {activePage > 3 && <span>...</span>}
          <TabButton number={activePage - 1} active={false} />
        </>
      )}
      {/*  */}
      {activePage > 1 && <TabButton number={activePage} active={true} />}
      {/*  */}
      {activePage < totalPages - 1 && (
        <>
          <TabButton number={activePage + 1} active={false} />
          {activePage < totalPages - 2 && <span>...</span>}
        </>
      )}
      {activePage < totalPages && (
        <TabButton number={totalPages} active={activePage === totalPages} />
      )}
    </div>
  );
};

export default Paginator;
