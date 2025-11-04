export function base64ToFile(
  base64String: string | null,
  filename: string
): File | null {
  if (base64String) {
    const arr: string[] = base64String.split(',');
    const mimeMatch: RegExpMatchArray | null = arr[0].match(/:(.*?);/);
    const mime: string = mimeMatch ? mimeMatch[1] : '';
    const bstr: string = atob(arr[1]);
    let n: number = bstr.length;
    const u8arr: Uint8Array = new Uint8Array(n);

    while (n--) {
      u8arr[n] = bstr.charCodeAt(n);
    }
    return new File([u8arr], filename, { type: mime });
  }
  return null;
}
