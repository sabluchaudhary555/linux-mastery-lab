import os
import stat


def get_file_type(path):
    if os.path.islink(path):
        if os.path.exists(path):
            return "SYMLINK", "🔗"
        else:
            return "BROKEN SYMLINK", "❌"

    s = os.stat(path)
    if stat.S_ISDIR(s.st_mode):
        return "DIRECTORY", "📁"
    elif s.st_nlink > 1:
        return f"HARD LINK ({s.st_nlink})", "🔵"
    else:
        return "REGULAR FILE", "📄"


def show_file_info(path):
    print(f"\n{'=' * 60}")
    print(f"FILE INFORMATION")
    print(f"{'=' * 60}")
    print(f"Path: {path}")

    try:
        if os.path.islink(path):
            target = os.readlink(path)
            ftype, icon = get_file_type(path)
            print(f"Type: {icon} {ftype}")
            print(f"Target: {target}")
            if os.path.exists(path):
                print(f"Resolved: {os.path.realpath(path)}")
            else:
                print("Status: BROKEN (target doesn't exist)")

            lstat = os.lstat(path)
            print(f"Link Size: {lstat.st_size} bytes")
        else:
            s = os.stat(path)
            ftype, icon = get_file_type(path)
            print(f"Type: {icon} {ftype}")
            print(f"Inode: {s.st_ino}")
            print(f"Hard Links: {s.st_nlink}")
            print(f"Size: {s.st_size:,} bytes")
            print(f"Permissions: {oct(stat.S_IMODE(s.st_mode))}")
            print(f"Owner UID: {s.st_uid}")
            print(f"Group GID: {s.st_gid}")
    except Exception as e:
        print(f"Error: {e}")

    print(f"{'=' * 60}\n")


def list_directory(path, max_items=20):
    print(f"\n📂 Directory: {path}")
    print(f"{'-' * 60}")

    try:
        items = sorted(os.listdir(path))[:max_items]
        for i, item in enumerate(items, 1):
            full_path = os.path.join(path, item)
            try:
                ftype, icon = get_file_type(full_path)
                print(f"{i:2}. {icon} {item}")
            except:
                print(f"{i:2}. ❓ {item} (permission denied)")

        if len(os.listdir(path)) > max_items:
            print(f"... and {len(os.listdir(path)) - max_items} more items")
    except Exception as e:
        print(f"Error: {e}")

    print(f"{'-' * 60}\n")


def find_hard_links(path, search_root=None):
    if os.path.islink(path):
        print("This is a symbolic link, not a hard link.")
        return

    try:
        inode = os.stat(path).st_ino
        nlinks = os.stat(path).st_nlink

        if nlinks == 1:
            print("This file has no other hard links.")
            return

        print(f"\n🔍 Searching for hard links (Inode: {inode}, Total links: {nlinks})")
        print(f"{'-' * 60}")

        if search_root is None:
            search_root = os.path.dirname(path)

        found = []
        for root, dirs, files in os.walk(search_root):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    if os.stat(fp).st_ino == inode:
                        found.append(fp)
                except:
                    pass

        for i, link in enumerate(found, 1):
            print(f"{i}. {link}")

        print(f"{'-' * 60}")
        print(f"Found {len(found)} hard link(s)\n")
    except Exception as e:
        print(f"Error: {e}")


def find_broken_symlinks(path):
    print(f"\n❌ Scanning for broken symlinks in: {path}")
    print(f"{'-' * 60}")

    broken = []
    for root, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            try:
                if os.path.islink(fp) and not os.path.exists(fp):
                    target = os.readlink(fp)
                    broken.append((fp, target))
            except:
                pass

    if broken:
        for i, (link, target) in enumerate(broken, 1):
            print(f"{i}. {link}")
            print(f"   → {target} (missing)")
    else:
        print("No broken symlinks found!")

    print(f"{'-' * 60}")
    print(f"Total broken: {len(broken)}\n")


def main():
    print("\n" + "=" * 60)
    print("LINKMANAGER - Hard & Soft Link Explorer".center(60))
    print("=" * 60)

    while True:
        print("\nOptions:")
        print("1. List directory")
        print("2. Show file details")
        print("3. Find hard links")
        print("4. Find broken symlinks")
        print("5. Exit")

        choice = input("\nEnter choice (1-5): ").strip()

        if choice == "1":
            path = input("Enter directory path (or press Enter for current): ").strip()
            if not path:
                path = os.getcwd()
            list_directory(path)

        elif choice == "2":
            path = input("Enter file/link path: ").strip()
            if os.path.exists(path) or os.path.islink(path):
                show_file_info(path)
            else:
                print("Path not found!")

        elif choice == "3":
            path = input("Enter file path: ").strip()
            if os.path.exists(path):
                find_hard_links(path)
            else:
                print("File not found!")

        elif choice == "4":
            path = input("Enter directory to scan (or press Enter for current): ").strip()
            if not path:
                path = os.getcwd()
            find_broken_symlinks(path)

        elif choice == "5":
            print("\nGoodbye!")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()