import inject from "@rollup/plugin-inject";
// import commonJs from "@rollup/plugin-commonjs";
import resolve from "@rollup/plugin-node-resolve";
import nodePolyfills from "rollup-plugin-polyfill-node";

/**
 * @type {import('rollup').RollupOptions}
 */

const emptyModule = {};

const nodeResolve = resolve({
  preferBuiltins: false,
  browser: true,
  mainFields: ["module", "browser"],
  skipSelf: true,
  custom: { "node-resolve": { isRequire: true } },
});

const browserifyAliases = {
  fs: "browserfs",
};

const browserify = {
  name: "browserify",
  resolve(source) {
    if (source in browserifyAliases) {
      if (browserifyAliases[source] === emptyModule) {
        return emptyModule;
      }
      return nodeResolve.resolveId(browserifyAliases[source], undefined);
    }
    if (source === emptyModule) return emptyModule;
  },
  load(id) {
    if (id === emptyModule) return emptyModule;
  },
};

// const browserfsPath = resolve("browserfs");
// const browserifyConfig = {
//   builtins: Object.assign({}, resolve("browserify/lib/builtins"), {
//     buffer: resolve("browserfs/dist/shims/buffer.js"),
//     fs: resolve("browserfs/dist/shims/fs.js"),
//     path: resolve("browserfs/dist/shims/path.js"),
//   }),
//   insertGlobalVars: {
//     process: function () {
//       return "require('browserfs/dist/shims/process.js')";
//     },
//     Buffer: function () {
//       return "require('buffer').Buffer";
//     },
//     BrowserFS: function () {
//       return "require('" + browserfsPath + "')";
//     },
//   },
// };

// const fsMkdir = {
//   name: "fs-mkdir",
//   transform(code, id) {
//     return code.replace(
//       /fs.readFileSync\(\s*__dirname\s*\+\s*'\/templates\/(.*)'\)/g,
//       (match, $1) => {
//         const tpl = path.join(
//           "./node_modules/browser-style-dictionary/lib/common/templates",
//           $1,
//         );
//         return JSON.stringify(fs.readFileSync(tpl, "utf8"));
//       },
//     );
//   },
// };

export default {
  input: {
    main: "./src/main.ts",
  },
  output: {
    // file: "bundle.js",
    format: "cjs",
    dir: "./dist",
  },
  plugins: [
    // commonJs({
    //   exclude: [
    //     "*socket.io-client*",
    //     "*engine.io*",
    //     "*socket.io-parser*",
    //     "*socket.js",
    //     "*create-torrent*",
    //     "*api*",
    //     "*axios*",
    //     "*AxiosError*",
    //     "*Axios*",
    //     "*devtools-api*",
    //   ],
    // }),
    browserify,
    inject({
      fs: ["browserfs", "*"],
    }),
    nodeResolve,
    nodePolyfills,
  ],
};
