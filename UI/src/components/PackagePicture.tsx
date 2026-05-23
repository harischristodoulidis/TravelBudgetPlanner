import { MapPin } from "lucide-react";
import { useEffect, useState } from "react";

interface PackagePictureProps {
  src: string;
  alt: string;
  className?: string;
}

const DEFAULT_IMAGE =
  "https://practicalwanderlust.com/wp-content/uploads/2017/02/How-to-Plan-a-Trip-Travel-Planning-Tips.jpg";

type Stage = "original" | "default" | "gradient";

export function PackagePicture({ src, alt, className }: PackagePictureProps) {
  const [stage, setStage] = useState<Stage>(src ? "original" : "default");

  useEffect(() => {
    setStage(src ? "original" : "default");
  }, [src]);

  if (stage === "gradient") {
    return (
      <div
        role="img"
        aria-label={alt}
        className={`${className ?? ""} flex items-center justify-center bg-linear-to-br from-brand-blue-soft to-brand-yellow`}
      >
        <MapPin
          aria-hidden
          strokeWidth={1.5}
          className="h-1/3 w-1/3 text-brand-blue/60"
        />
      </div>
    );
  }

  return (
    <img
      src={stage === "original" ? src : DEFAULT_IMAGE}
      alt={alt}
      loading="lazy"
      className={className}
      onError={() =>
        setStage((s) => (s === "original" ? "default" : "gradient"))
      }
    />
  );
}
