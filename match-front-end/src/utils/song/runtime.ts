import exp from "constants";

const convertRuntime = (runtime: number) => {
  const minutes = Math.floor(runtime / 60);
  const seconds = runtime % 60;
  return `${minutes}:${seconds < 10 ? `0${seconds}` : seconds}`;
};

export default convertRuntime;
