import { useEffect, useState } from "react";

interface PackagePictureProps {
  src: string;
  alt: string;
  className?: string;
}

export function PackagePicture({ src, alt, className }: PackagePictureProps) {
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    setFailed(false);
  }, [src]);

  if (!src || failed) {
    return (
      <div
        role="img"
        aria-label={alt}
        className={`${className ?? ""} bg-[#F5D87A]`}
      />
    );
  }

  return (
    <img
      src={src}
      alt={alt}
      loading="lazy"
      className={className}
      onError={() => setFailed(true)}
    />
  );
}
