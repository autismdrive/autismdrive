/**
 * Safely stringify an object, handling circular references and other issues.
 * https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Errors/Cyclic_object_value#examples
 */
export const safeStringify = (obj: any) => {
  const replacer = () => {
    const ancestors = [];
    return function (key, value) {
      if (typeof value !== 'object' || value === null) {
        return value;
      }
      // `this` is the object that value is contained in,
      // i.e., its direct parent.
      while (ancestors.length > 0 && ancestors.at(-1) !== this) {
        ancestors.pop();
      }
      if (ancestors.includes(value)) {
        return '[Circular]';
      }
      ancestors.push(value);
      return value;
    };
  };

  try {
    return JSON.stringify(obj, replacer());
  } catch (error) {
    throw error;
  }
};
