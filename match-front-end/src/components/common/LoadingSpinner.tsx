import React from "react";
import { ImSpinner2 } from "react-icons/im";

const LoadingSpinner = () => {
  return (
    <div className="flex justify-center items-center h-screen">
      <div className="animate-spin">
        <ImSpinner2 className="text-4xl" />
      </div>
    </div>
  );
};

export default LoadingSpinner;
