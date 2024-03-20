export const snakeToUpperCase = function (s: string) {
  return s.replace(/([-_][a-z]|^[a-z])/gi, $1 => {
    return $1.toUpperCase().replace('-', ' ').replace('_', ' ');
  });
};
