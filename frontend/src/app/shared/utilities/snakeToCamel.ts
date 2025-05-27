// Convert snake to camelCase.
// Thanks to http://jsfiddle.net/ms734bqn/1/
const isObject = function (o): boolean {
  return o === Object(o) && !Array.isArray(o) && typeof o !== 'function';
};

export const toCamel = function (s: string) {
  return s.replace(/([-_][a-z])/gi, $1 => {
    return $1.toUpperCase().replace('-', '').replace('_', '');
  });
};

export const keysToCamel = function (o) {
  if (isObject(o)) {
    const n = {};

    Object.keys(o).forEach(k => {
      n[toCamel(k)] = keysToCamel(o[k]);
    });

    return n;
  } else if (Array.isArray(o)) {
    return o.map(i => {
      return keysToCamel(i);
    });
  }

  return o;
};
