module.exports = {
  root: true,
  env: {
    es2021: true,
  },
  globals: {
    defineProps: "readonly",
    defineEmits: "readonly",
    withDefaults: "readonly",
  },
  extends: [
    "@vue/typescript/recommended",
    "eslint:recommended",
    "plugin:vue/vue3-recommended",
    "prettier",
  ],
  parser: "vue-eslint-parser",
  parserOptions: {
    parser: {
      js: "espree",
      ts: "@typescript-eslint/parser",
      "<template>": "espree",
    },
  },
  ignorePatterns: ["webtorrent.min.js"],
  rules: {
    "vue/multi-word-component-names": 0,
  },
};
