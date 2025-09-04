import React, { useRef, useEffect } from 'react';

/**
 * VideoHeroSection displays a promotional video with auto-play/pause based on visibility.
 */
const VideoHeroSection: React.FC = () => {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;
    const handlePlay = (entries: IntersectionObserverEntry[]) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          video.play();
        } else {
          video.pause();
        }
      });
    };
    const observer = new window.IntersectionObserver(handlePlay, {
      threshold: 0.5,
    });
    observer.observe(video);
    return () => {
      observer.disconnect();
    };
  }, []);

  return (
    <div className="relative min-h-[400px] w-full flex flex-col items-center justify-center text-[#14213d] rounded-2xl mb-10">
      <div className="container mx-auto z-10 text-center py-6">
        <h5 className="text-lg sm:text-2xl md:text-3xl mb-6">
          Securely store receipts, get warranty reminders, and track your purchases with ease
        </h5>
        {/* Promotional Video Section */}
        <div className="w-full max-w-full h-[300px] sm:h-[400px] md:h-[520px] rounded-2xl overflow-hidden shadow-lg mx-auto mb-2 flex items-center justify-center">
          <video
            ref={videoRef}
            src="/assets/MicrosoftTeams-video (2).mp4"
            loop
            muted
            controls
            className="w-[120%] h-full max-h-full block bg-black object-cover"
          />
        </div>
      </div>
    </div>
  );
};

export default VideoHeroSection; 