declare module "*.jpg" {
  const value: any;
  export = value;
}
declare module "*.png" {
  const value: any;
  export = value;
}

declare module "*.svg" {
  const value: any;
  export = value;
}

declare module "ya-translate" {
  const translate: () => translator;
  export = translate;
}

declare type translator = (text: string, language?: string) => Promise<TranslatedObject>;

declare type TranslatedObject = {
  code: number;
  detected: { lang: string };
  lang: string;
  text: string[];
};
