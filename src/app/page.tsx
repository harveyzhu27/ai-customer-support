import HeadstarterAssistant from '@/components/HeadstarterAssistant';
import Link from 'next/link';

export default function Home() {
  return (
    <div>
      <HeadstarterAssistant />
      
      {/* Test API Link */}
      <div className="fixed bottom-4 right-4 z-50">
        <Link 
          href="/test-api"
          className="inline-flex items-center px-4 py-2 bg-orange-500 hover:bg-orange-600 text-white rounded-lg text-sm font-medium transition-colors shadow-lg"
        >
          🧪 Test API
        </Link>
      </div>
    </div>
  );
}
