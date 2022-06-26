import BrowserFS from "browserfs";
import { BFSOneArgCallback } from "browserfs/dist/node/core/file_system";

export const fs = {
  mkdir: (path: string, mode?: any, cb?: BFSOneArgCallback | undefined): void =>
    BrowserFS.BFSRequire("fs").mkdir(path, mode, cb),
};
