export const mockWindowFactory = (options?: unknown) => {
  const defaultWindow = {
    dataLayer: [],
    innerWidth: 0,
    innerHeight: 0,
    addEventListener: () => {},
    removeEventListener: () => {},
    setInterval: () => {},
    clearInterval: () => {},
    document: {
      body: {
        appendChild: () => {},
        removeChild: () => {},
      },
    },
    open: () => {},
    scroll: () => {},
    scrollTo: () => {},
    location: {
      origin: '',
    },
    scrollY: 0,
  } as unknown as Partial<Window & typeof globalThis>;

  return options
    ? {
        ...defaultWindow,
        ...(options as unknown as Partial<Window & typeof globalThis>),
      }
    : ({...defaultWindow} as unknown as Window & typeof globalThis);
};

export const mockWindow = mockWindowFactory();
